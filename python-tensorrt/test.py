import tensorrt as trt
# 判断版本
check_version(trt.__version__, '7.0.0', hard=True)  # require tensorrt>=7.0.0
if device.type == 'cpu':
    device = torch.device('cuda:0')
# 1.创建一个Binding对象，该对象包含'name', 'dtype', 'shape', 'data', 'ptr'这些属性
Binding = namedtuple('Binding', ('name', 'dtype', 'shape', 'data', 'ptr'))
logger = trt.Logger(trt.Logger.INFO)
# 2.读取engine文件并记录log
with open(w, 'rb') as f, trt.Runtime(logger) as runtime:
    # 将engine进行反序列化，这里的model就是反序列化中的model
    model = runtime.deserialize_cuda_engine(f.read())  # model <class 'tensorrt.tensorrt.ICudaEngine'> num_bindings=2,num_layers=163
# 3.构建可执行的context(上下文：记录执行任务所需要的相关信息)
context = model.create_execution_context()  # <IExecutionContext>
bindings = OrderedDict()
output_names = []
fp16 = False  # default updated below
dynamic = False
for i in range(model.num_bindings):
    name = model.get_binding_name(i) # 获得输入输出的名字"images","output0"
    dtype = trt.nptype(model.get_binding_dtype(i))
    if model.binding_is_input(i):  # 判断是否为输入
        if -1 in tuple(model.get_binding_shape(i)):  # dynamic get_binding_shape(0)->(1,3,640,640) get_binding_shape(1)->(1,25200,85)
            dynamic = True
            context.set_binding_shape(i, tuple(model.get_profile_shape(0, i)[2]))
        if dtype == np.float16:
            fp16 = True
    else:  # output
        output_names.append(name)  # 放入输出名字 output_names = ['output0']
    shape = tuple(context.get_binding_shape(i))  # 记录输入输出shape
    im = torch.from_numpy(np.empty(shape, dtype=dtype)).to(device)  # 创建一个全0的与输入或输出shape相同的tensor
    bindings[name] = Binding(name, dtype, shape, im, int(im.data_ptr()))  # 放入之前创建的对象中
binding_addrs = OrderedDict((n, d.ptr) for n, d in bindings.items())  # 提取name以及对应的Binding
batch_size = bindings['images'].shape[0]  # if dynamic, this is instead max batch size